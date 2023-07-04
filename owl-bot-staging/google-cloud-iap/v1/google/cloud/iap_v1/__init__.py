# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.cloud.iap_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.identity_aware_proxy_admin_service import IdentityAwareProxyAdminServiceClient
from .services.identity_aware_proxy_admin_service import IdentityAwareProxyAdminServiceAsyncClient
from .services.identity_aware_proxy_o_auth_service import IdentityAwareProxyOAuthServiceClient
from .services.identity_aware_proxy_o_auth_service import IdentityAwareProxyOAuthServiceAsyncClient

from .types.service import AccessDeniedPageSettings
from .types.service import AccessSettings
from .types.service import AllowedDomainsSettings
from .types.service import ApplicationSettings
from .types.service import AttributePropagationSettings
from .types.service import Brand
from .types.service import CorsSettings
from .types.service import CreateBrandRequest
from .types.service import CreateIdentityAwareProxyClientRequest
from .types.service import CreateTunnelDestGroupRequest
from .types.service import CsmSettings
from .types.service import DeleteIdentityAwareProxyClientRequest
from .types.service import DeleteTunnelDestGroupRequest
from .types.service import GcipSettings
from .types.service import GetBrandRequest
from .types.service import GetIapSettingsRequest
from .types.service import GetIdentityAwareProxyClientRequest
from .types.service import GetTunnelDestGroupRequest
from .types.service import IapSettings
from .types.service import IdentityAwareProxyClient
from .types.service import ListBrandsRequest
from .types.service import ListBrandsResponse
from .types.service import ListIdentityAwareProxyClientsRequest
from .types.service import ListIdentityAwareProxyClientsResponse
from .types.service import ListTunnelDestGroupsRequest
from .types.service import ListTunnelDestGroupsResponse
from .types.service import OAuthSettings
from .types.service import ReauthSettings
from .types.service import ResetIdentityAwareProxyClientSecretRequest
from .types.service import TunnelDestGroup
from .types.service import UpdateIapSettingsRequest
from .types.service import UpdateTunnelDestGroupRequest

__all__ = (
    'IdentityAwareProxyAdminServiceAsyncClient',
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
'IdentityAwareProxyAdminServiceClient',
'IdentityAwareProxyClient',
'IdentityAwareProxyOAuthServiceClient',
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
