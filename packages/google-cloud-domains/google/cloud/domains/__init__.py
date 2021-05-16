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

from google.cloud.domains_v1beta1.services.domains.client import DomainsClient
from google.cloud.domains_v1beta1.services.domains.async_client import (
    DomainsAsyncClient,
)

from google.cloud.domains_v1beta1.types.domains import AuthorizationCode
from google.cloud.domains_v1beta1.types.domains import ConfigureContactSettingsRequest
from google.cloud.domains_v1beta1.types.domains import ConfigureDnsSettingsRequest
from google.cloud.domains_v1beta1.types.domains import (
    ConfigureManagementSettingsRequest,
)
from google.cloud.domains_v1beta1.types.domains import ContactSettings
from google.cloud.domains_v1beta1.types.domains import DeleteRegistrationRequest
from google.cloud.domains_v1beta1.types.domains import DnsSettings
from google.cloud.domains_v1beta1.types.domains import ExportRegistrationRequest
from google.cloud.domains_v1beta1.types.domains import GetRegistrationRequest
from google.cloud.domains_v1beta1.types.domains import ListRegistrationsRequest
from google.cloud.domains_v1beta1.types.domains import ListRegistrationsResponse
from google.cloud.domains_v1beta1.types.domains import ManagementSettings
from google.cloud.domains_v1beta1.types.domains import OperationMetadata
from google.cloud.domains_v1beta1.types.domains import RegisterDomainRequest
from google.cloud.domains_v1beta1.types.domains import RegisterParameters
from google.cloud.domains_v1beta1.types.domains import Registration
from google.cloud.domains_v1beta1.types.domains import ResetAuthorizationCodeRequest
from google.cloud.domains_v1beta1.types.domains import RetrieveAuthorizationCodeRequest
from google.cloud.domains_v1beta1.types.domains import RetrieveRegisterParametersRequest
from google.cloud.domains_v1beta1.types.domains import (
    RetrieveRegisterParametersResponse,
)
from google.cloud.domains_v1beta1.types.domains import SearchDomainsRequest
from google.cloud.domains_v1beta1.types.domains import SearchDomainsResponse
from google.cloud.domains_v1beta1.types.domains import UpdateRegistrationRequest
from google.cloud.domains_v1beta1.types.domains import ContactNotice
from google.cloud.domains_v1beta1.types.domains import ContactPrivacy
from google.cloud.domains_v1beta1.types.domains import DomainNotice
from google.cloud.domains_v1beta1.types.domains import TransferLockState

__all__ = (
    "DomainsClient",
    "DomainsAsyncClient",
    "AuthorizationCode",
    "ConfigureContactSettingsRequest",
    "ConfigureDnsSettingsRequest",
    "ConfigureManagementSettingsRequest",
    "ContactSettings",
    "DeleteRegistrationRequest",
    "DnsSettings",
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
    "UpdateRegistrationRequest",
    "ContactNotice",
    "ContactPrivacy",
    "DomainNotice",
    "TransferLockState",
)
