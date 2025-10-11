# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.network_security_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.address_group_service import AddressGroupServiceClient
from .services.address_group_service import AddressGroupServiceAsyncClient
from .services.network_security import NetworkSecurityClient
from .services.network_security import NetworkSecurityAsyncClient
from .services.organization_address_group_service import OrganizationAddressGroupServiceClient
from .services.organization_address_group_service import OrganizationAddressGroupServiceAsyncClient

from .types.address_group import AddAddressGroupItemsRequest
from .types.address_group import AddressGroup
from .types.address_group import CloneAddressGroupItemsRequest
from .types.address_group import CreateAddressGroupRequest
from .types.address_group import DeleteAddressGroupRequest
from .types.address_group import GetAddressGroupRequest
from .types.address_group import ListAddressGroupReferencesRequest
from .types.address_group import ListAddressGroupReferencesResponse
from .types.address_group import ListAddressGroupsRequest
from .types.address_group import ListAddressGroupsResponse
from .types.address_group import RemoveAddressGroupItemsRequest
from .types.address_group import UpdateAddressGroupRequest
from .types.authorization_policy import AuthorizationPolicy
from .types.authorization_policy import CreateAuthorizationPolicyRequest
from .types.authorization_policy import DeleteAuthorizationPolicyRequest
from .types.authorization_policy import GetAuthorizationPolicyRequest
from .types.authorization_policy import ListAuthorizationPoliciesRequest
from .types.authorization_policy import ListAuthorizationPoliciesResponse
from .types.authorization_policy import UpdateAuthorizationPolicyRequest
from .types.client_tls_policy import ClientTlsPolicy
from .types.client_tls_policy import CreateClientTlsPolicyRequest
from .types.client_tls_policy import DeleteClientTlsPolicyRequest
from .types.client_tls_policy import GetClientTlsPolicyRequest
from .types.client_tls_policy import ListClientTlsPoliciesRequest
from .types.client_tls_policy import ListClientTlsPoliciesResponse
from .types.client_tls_policy import UpdateClientTlsPolicyRequest
from .types.common import OperationMetadata
from .types.server_tls_policy import CreateServerTlsPolicyRequest
from .types.server_tls_policy import DeleteServerTlsPolicyRequest
from .types.server_tls_policy import GetServerTlsPolicyRequest
from .types.server_tls_policy import ListServerTlsPoliciesRequest
from .types.server_tls_policy import ListServerTlsPoliciesResponse
from .types.server_tls_policy import ServerTlsPolicy
from .types.server_tls_policy import UpdateServerTlsPolicyRequest
from .types.tls import CertificateProvider
from .types.tls import CertificateProviderInstance
from .types.tls import GrpcEndpoint
from .types.tls import ValidationCA

__all__ = (
    'AddressGroupServiceAsyncClient',
    'NetworkSecurityAsyncClient',
    'OrganizationAddressGroupServiceAsyncClient',
'AddAddressGroupItemsRequest',
'AddressGroup',
'AddressGroupServiceClient',
'AuthorizationPolicy',
'CertificateProvider',
'CertificateProviderInstance',
'ClientTlsPolicy',
'CloneAddressGroupItemsRequest',
'CreateAddressGroupRequest',
'CreateAuthorizationPolicyRequest',
'CreateClientTlsPolicyRequest',
'CreateServerTlsPolicyRequest',
'DeleteAddressGroupRequest',
'DeleteAuthorizationPolicyRequest',
'DeleteClientTlsPolicyRequest',
'DeleteServerTlsPolicyRequest',
'GetAddressGroupRequest',
'GetAuthorizationPolicyRequest',
'GetClientTlsPolicyRequest',
'GetServerTlsPolicyRequest',
'GrpcEndpoint',
'ListAddressGroupReferencesRequest',
'ListAddressGroupReferencesResponse',
'ListAddressGroupsRequest',
'ListAddressGroupsResponse',
'ListAuthorizationPoliciesRequest',
'ListAuthorizationPoliciesResponse',
'ListClientTlsPoliciesRequest',
'ListClientTlsPoliciesResponse',
'ListServerTlsPoliciesRequest',
'ListServerTlsPoliciesResponse',
'NetworkSecurityClient',
'OperationMetadata',
'OrganizationAddressGroupServiceClient',
'RemoveAddressGroupItemsRequest',
'ServerTlsPolicy',
'UpdateAddressGroupRequest',
'UpdateAuthorizationPolicyRequest',
'UpdateClientTlsPolicyRequest',
'UpdateServerTlsPolicyRequest',
'ValidationCA',
)
