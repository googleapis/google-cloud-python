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

from .services.domains import DomainsClient
from .services.domains import DomainsAsyncClient

from .types.domains import AuthorizationCode
from .types.domains import ConfigureContactSettingsRequest
from .types.domains import ConfigureDnsSettingsRequest
from .types.domains import ConfigureManagementSettingsRequest
from .types.domains import ContactSettings
from .types.domains import DeleteRegistrationRequest
from .types.domains import DnsSettings
from .types.domains import ExportRegistrationRequest
from .types.domains import GetRegistrationRequest
from .types.domains import ListRegistrationsRequest
from .types.domains import ListRegistrationsResponse
from .types.domains import ManagementSettings
from .types.domains import OperationMetadata
from .types.domains import RegisterDomainRequest
from .types.domains import RegisterParameters
from .types.domains import Registration
from .types.domains import ResetAuthorizationCodeRequest
from .types.domains import RetrieveAuthorizationCodeRequest
from .types.domains import RetrieveRegisterParametersRequest
from .types.domains import RetrieveRegisterParametersResponse
from .types.domains import SearchDomainsRequest
from .types.domains import SearchDomainsResponse
from .types.domains import UpdateRegistrationRequest
from .types.domains import ContactNotice
from .types.domains import ContactPrivacy
from .types.domains import DomainNotice
from .types.domains import TransferLockState

__all__ = (
    "DomainsAsyncClient",
    "AuthorizationCode",
    "ConfigureContactSettingsRequest",
    "ConfigureDnsSettingsRequest",
    "ConfigureManagementSettingsRequest",
    "ContactNotice",
    "ContactPrivacy",
    "ContactSettings",
    "DeleteRegistrationRequest",
    "DnsSettings",
    "DomainNotice",
    "DomainsClient",
    "ExportRegistrationRequest",
    "GetRegistrationRequest",
    "ListRegistrationsRequest",
    "ListRegistrationsResponse",
    "ManagementSettings",
    "OperationMetadata",
    "RegisterDomainRequest",
    "RegisterParameters",
    "Registration",
    "ResetAuthorizationCodeRequest",
    "RetrieveAuthorizationCodeRequest",
    "RetrieveRegisterParametersRequest",
    "RetrieveRegisterParametersResponse",
    "SearchDomainsRequest",
    "SearchDomainsResponse",
    "TransferLockState",
    "UpdateRegistrationRequest",
)
