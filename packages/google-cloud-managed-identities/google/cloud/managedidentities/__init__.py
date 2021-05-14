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

from google.cloud.managedidentities_v1.services.managed_identities_service.client import (
    ManagedIdentitiesServiceClient,
)
from google.cloud.managedidentities_v1.services.managed_identities_service.async_client import (
    ManagedIdentitiesServiceAsyncClient,
)

from google.cloud.managedidentities_v1.types.managed_identities_service import (
    AttachTrustRequest,
)
from google.cloud.managedidentities_v1.types.managed_identities_service import (
    CreateMicrosoftAdDomainRequest,
)
from google.cloud.managedidentities_v1.types.managed_identities_service import (
    DeleteDomainRequest,
)
from google.cloud.managedidentities_v1.types.managed_identities_service import (
    DetachTrustRequest,
)
from google.cloud.managedidentities_v1.types.managed_identities_service import (
    GetDomainRequest,
)
from google.cloud.managedidentities_v1.types.managed_identities_service import (
    ListDomainsRequest,
)
from google.cloud.managedidentities_v1.types.managed_identities_service import (
    ListDomainsResponse,
)
from google.cloud.managedidentities_v1.types.managed_identities_service import (
    OpMetadata,
)
from google.cloud.managedidentities_v1.types.managed_identities_service import (
    ReconfigureTrustRequest,
)
from google.cloud.managedidentities_v1.types.managed_identities_service import (
    ResetAdminPasswordRequest,
)
from google.cloud.managedidentities_v1.types.managed_identities_service import (
    ResetAdminPasswordResponse,
)
from google.cloud.managedidentities_v1.types.managed_identities_service import (
    UpdateDomainRequest,
)
from google.cloud.managedidentities_v1.types.managed_identities_service import (
    ValidateTrustRequest,
)
from google.cloud.managedidentities_v1.types.resource import Domain
from google.cloud.managedidentities_v1.types.resource import Trust

__all__ = (
    "ManagedIdentitiesServiceClient",
    "ManagedIdentitiesServiceAsyncClient",
    "AttachTrustRequest",
    "CreateMicrosoftAdDomainRequest",
    "DeleteDomainRequest",
    "DetachTrustRequest",
    "GetDomainRequest",
    "ListDomainsRequest",
    "ListDomainsResponse",
    "OpMetadata",
    "ReconfigureTrustRequest",
    "ResetAdminPasswordRequest",
    "ResetAdminPasswordResponse",
    "UpdateDomainRequest",
    "ValidateTrustRequest",
    "Domain",
    "Trust",
)
