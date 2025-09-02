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
from google.cloud.network_security import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.network_security_v1.services.address_group_service.client import AddressGroupServiceClient
from google.cloud.network_security_v1.services.address_group_service.async_client import AddressGroupServiceAsyncClient
from google.cloud.network_security_v1.services.network_security.client import NetworkSecurityClient
from google.cloud.network_security_v1.services.network_security.async_client import NetworkSecurityAsyncClient
from google.cloud.network_security_v1.services.organization_address_group_service.client import OrganizationAddressGroupServiceClient
from google.cloud.network_security_v1.services.organization_address_group_service.async_client import OrganizationAddressGroupServiceAsyncClient

from google.cloud.network_security_v1.types.address_group import AddAddressGroupItemsRequest
from google.cloud.network_security_v1.types.address_group import AddressGroup
from google.cloud.network_security_v1.types.address_group import CloneAddressGroupItemsRequest
from google.cloud.network_security_v1.types.address_group import CreateAddressGroupRequest
from google.cloud.network_security_v1.types.address_group import DeleteAddressGroupRequest
from google.cloud.network_security_v1.types.address_group import GetAddressGroupRequest
from google.cloud.network_security_v1.types.address_group import ListAddressGroupReferencesRequest
from google.cloud.network_security_v1.types.address_group import ListAddressGroupReferencesResponse
from google.cloud.network_security_v1.types.address_group import ListAddressGroupsRequest
from google.cloud.network_security_v1.types.address_group import ListAddressGroupsResponse
from google.cloud.network_security_v1.types.address_group import RemoveAddressGroupItemsRequest
from google.cloud.network_security_v1.types.address_group import UpdateAddressGroupRequest
from google.cloud.network_security_v1.types.authorization_policy import AuthorizationPolicy
from google.cloud.network_security_v1.types.authorization_policy import CreateAuthorizationPolicyRequest
from google.cloud.network_security_v1.types.authorization_policy import DeleteAuthorizationPolicyRequest
from google.cloud.network_security_v1.types.authorization_policy import GetAuthorizationPolicyRequest
from google.cloud.network_security_v1.types.authorization_policy import ListAuthorizationPoliciesRequest
from google.cloud.network_security_v1.types.authorization_policy import ListAuthorizationPoliciesResponse
from google.cloud.network_security_v1.types.authorization_policy import UpdateAuthorizationPolicyRequest
from google.cloud.network_security_v1.types.client_tls_policy import ClientTlsPolicy
from google.cloud.network_security_v1.types.client_tls_policy import CreateClientTlsPolicyRequest
from google.cloud.network_security_v1.types.client_tls_policy import DeleteClientTlsPolicyRequest
from google.cloud.network_security_v1.types.client_tls_policy import GetClientTlsPolicyRequest
from google.cloud.network_security_v1.types.client_tls_policy import ListClientTlsPoliciesRequest
from google.cloud.network_security_v1.types.client_tls_policy import ListClientTlsPoliciesResponse
from google.cloud.network_security_v1.types.client_tls_policy import UpdateClientTlsPolicyRequest
from google.cloud.network_security_v1.types.common import OperationMetadata
from google.cloud.network_security_v1.types.server_tls_policy import CreateServerTlsPolicyRequest
from google.cloud.network_security_v1.types.server_tls_policy import DeleteServerTlsPolicyRequest
from google.cloud.network_security_v1.types.server_tls_policy import GetServerTlsPolicyRequest
from google.cloud.network_security_v1.types.server_tls_policy import ListServerTlsPoliciesRequest
from google.cloud.network_security_v1.types.server_tls_policy import ListServerTlsPoliciesResponse
from google.cloud.network_security_v1.types.server_tls_policy import ServerTlsPolicy
from google.cloud.network_security_v1.types.server_tls_policy import UpdateServerTlsPolicyRequest
from google.cloud.network_security_v1.types.tls import CertificateProvider
from google.cloud.network_security_v1.types.tls import CertificateProviderInstance
from google.cloud.network_security_v1.types.tls import GrpcEndpoint
from google.cloud.network_security_v1.types.tls import ValidationCA

__all__ = ('AddressGroupServiceClient',
    'AddressGroupServiceAsyncClient',
    'NetworkSecurityClient',
    'NetworkSecurityAsyncClient',
    'OrganizationAddressGroupServiceClient',
    'OrganizationAddressGroupServiceAsyncClient',
    'AddAddressGroupItemsRequest',
    'AddressGroup',
    'CloneAddressGroupItemsRequest',
    'CreateAddressGroupRequest',
    'DeleteAddressGroupRequest',
    'GetAddressGroupRequest',
    'ListAddressGroupReferencesRequest',
    'ListAddressGroupReferencesResponse',
    'ListAddressGroupsRequest',
    'ListAddressGroupsResponse',
    'RemoveAddressGroupItemsRequest',
    'UpdateAddressGroupRequest',
    'AuthorizationPolicy',
    'CreateAuthorizationPolicyRequest',
    'DeleteAuthorizationPolicyRequest',
    'GetAuthorizationPolicyRequest',
    'ListAuthorizationPoliciesRequest',
    'ListAuthorizationPoliciesResponse',
    'UpdateAuthorizationPolicyRequest',
    'ClientTlsPolicy',
    'CreateClientTlsPolicyRequest',
    'DeleteClientTlsPolicyRequest',
    'GetClientTlsPolicyRequest',
    'ListClientTlsPoliciesRequest',
    'ListClientTlsPoliciesResponse',
    'UpdateClientTlsPolicyRequest',
    'OperationMetadata',
    'CreateServerTlsPolicyRequest',
    'DeleteServerTlsPolicyRequest',
    'GetServerTlsPolicyRequest',
    'ListServerTlsPoliciesRequest',
    'ListServerTlsPoliciesResponse',
    'ServerTlsPolicy',
    'UpdateServerTlsPolicyRequest',
    'CertificateProvider',
    'CertificateProviderInstance',
    'GrpcEndpoint',
    'ValidationCA',
)
