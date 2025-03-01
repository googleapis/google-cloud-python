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
from google.cloud.iap import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.iap_v1.services.identity_aware_proxy_admin_service.client import IdentityAwareProxyAdminServiceClient
from google.cloud.iap_v1.services.identity_aware_proxy_admin_service.async_client import IdentityAwareProxyAdminServiceAsyncClient
from google.cloud.iap_v1.services.identity_aware_proxy_o_auth_service.client import IdentityAwareProxyOAuthServiceClient
from google.cloud.iap_v1.services.identity_aware_proxy_o_auth_service.async_client import IdentityAwareProxyOAuthServiceAsyncClient

from google.cloud.iap_v1.types.service import AccessDeniedPageSettings
from google.cloud.iap_v1.types.service import AccessSettings
from google.cloud.iap_v1.types.service import AllowedDomainsSettings
from google.cloud.iap_v1.types.service import ApplicationSettings
from google.cloud.iap_v1.types.service import AttributePropagationSettings
from google.cloud.iap_v1.types.service import Brand
from google.cloud.iap_v1.types.service import CorsSettings
from google.cloud.iap_v1.types.service import CreateBrandRequest
from google.cloud.iap_v1.types.service import CreateIdentityAwareProxyClientRequest
from google.cloud.iap_v1.types.service import CreateTunnelDestGroupRequest
from google.cloud.iap_v1.types.service import CsmSettings
from google.cloud.iap_v1.types.service import DeleteIdentityAwareProxyClientRequest
from google.cloud.iap_v1.types.service import DeleteTunnelDestGroupRequest
from google.cloud.iap_v1.types.service import GcipSettings
from google.cloud.iap_v1.types.service import GetBrandRequest
from google.cloud.iap_v1.types.service import GetIapSettingsRequest
from google.cloud.iap_v1.types.service import GetIdentityAwareProxyClientRequest
from google.cloud.iap_v1.types.service import GetTunnelDestGroupRequest
from google.cloud.iap_v1.types.service import IapSettings
from google.cloud.iap_v1.types.service import IdentityAwareProxyClient
from google.cloud.iap_v1.types.service import ListBrandsRequest
from google.cloud.iap_v1.types.service import ListBrandsResponse
from google.cloud.iap_v1.types.service import ListIdentityAwareProxyClientsRequest
from google.cloud.iap_v1.types.service import ListIdentityAwareProxyClientsResponse
from google.cloud.iap_v1.types.service import ListTunnelDestGroupsRequest
from google.cloud.iap_v1.types.service import ListTunnelDestGroupsResponse
from google.cloud.iap_v1.types.service import OAuthSettings
from google.cloud.iap_v1.types.service import ReauthSettings
from google.cloud.iap_v1.types.service import ResetIdentityAwareProxyClientSecretRequest
from google.cloud.iap_v1.types.service import TunnelDestGroup
from google.cloud.iap_v1.types.service import UpdateIapSettingsRequest
from google.cloud.iap_v1.types.service import UpdateTunnelDestGroupRequest

__all__ = ('IdentityAwareProxyAdminServiceClient',
    'IdentityAwareProxyAdminServiceAsyncClient',
    'IdentityAwareProxyOAuthServiceClient',
    'IdentityAwareProxyOAuthServiceAsyncClient',
    'AccessDeniedPageSettings',
    'AccessSettings',
    'AllowedDomainsSettings',
    'ApplicationSettings',
    'AttributePropagationSettings',
    'Brand',
    'CorsSettings',
    'CreateBrandRequest',
    'CreateIdentityAwareProxyClientRequest',
    'CreateTunnelDestGroupRequest',
    'CsmSettings',
    'DeleteIdentityAwareProxyClientRequest',
    'DeleteTunnelDestGroupRequest',
    'GcipSettings',
    'GetBrandRequest',
    'GetIapSettingsRequest',
    'GetIdentityAwareProxyClientRequest',
    'GetTunnelDestGroupRequest',
    'IapSettings',
    'IdentityAwareProxyClient',
    'ListBrandsRequest',
    'ListBrandsResponse',
    'ListIdentityAwareProxyClientsRequest',
    'ListIdentityAwareProxyClientsResponse',
    'ListTunnelDestGroupsRequest',
    'ListTunnelDestGroupsResponse',
    'OAuthSettings',
    'ReauthSettings',
    'ResetIdentityAwareProxyClientSecretRequest',
    'TunnelDestGroup',
    'UpdateIapSettingsRequest',
    'UpdateTunnelDestGroupRequest',
)
